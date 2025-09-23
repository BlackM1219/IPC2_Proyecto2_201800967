from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from parsers.xml_parser import XMLParser
from simulator.simulator import Simulator
from generators.salida_writer import SalidaWriter
from generators.graphviz_gen import GraphvizGenerator
import os
from config import UPLOAD_FOLDER




def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'dev-secret'


    parser = XMLParser()


    # memoria simple: carga actual
    app.config['data'] = None
    app.config['sim_results'] = None


    @app.route('/')
    def index():
        data = app.config.get('data')
        return render_template('index.html', data=data)


    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files.get('file')
        if not file:
            flash('No file selected')
            return redirect(url_for('index'))
        filename = file.filename
        if not filename.lower().endswith('.xml'):
            flash('Only XML files allowed')
            return redirect(url_for('index'))
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        data = parser.parse(path)
        app.config['data'] = data
        flash('File loaded')
        return redirect(url_for('index'))


    @app.route('/simulate', methods=['POST'])
    def simulate():
        data = app.config.get('data')
        if not data:
            flash('No configuration loaded')
            return redirect(url_for('index'))
        invernadero_nombre = request.form.get('invernadero')
        plan_nombre = request.form.get('plan')
        t_str = request.form.get('t')
        try:
            t = int(t_str) if t_str else None
        except:
            t = None
        sim = Simulator(data)
        results = sim.run_plan(invernadero_nombre, plan_nombre)
        app.config['sim_results'] = results
        # write salida.xml
        writer = SalidaWriter()
        salida_path = writer.write(results, os.path.join(app.config['UPLOAD_FOLDER'], 'salida.xml'))
        # graph
        graphgen = GraphvizGenerator()
        dot_path = graphgen.generate_tda_graph(results, time_t=t, outpath=os.path.join(app.config['UPLOAD_FOLDER'], 'tda.dot'))
        flash(f'Simulation complete. salida saved to {salida_path}')
        return render_template('report_invernadero.html', results=results, t=t)
    @app.route('/download/salida')
    def download_salida():
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'salida.xml')
        if os.path.exists(path):
            return send_file(path, as_attachment=True)
        flash('No salida.xml available')
        return redirect(url_for('index'))
    return app
    