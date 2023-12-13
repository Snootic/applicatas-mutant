import subprocess
import ttkbootstrap as ttk
import os, sys
from telas import app
from datetime import datetime
import shutil

python_path = sys.executable
pyinstaller_path = python_path.replace("python", "pyinstaller")
spec_path = os.path.abspath('build.spec')
versao_path = os.path.abspath('VERSION')
data_path = os.path.abspath('data')
dist_version_path = os.path.join(os.getcwd(), 'dist/VERSION')
dist_data_path = os.path.join(os.getcwd(), 'dist/data')
python_version = sys.version
license_path = os.path.abspath('LICENSE')
dist_license_path =  os.path.join(os.getcwd(), 'dist/LICENSE')

def run():
    version = versao_var.get()
    if version == '':
        label.config(text='Insira uma versão válida')
        versao.config(bootstyle="Danger")
        root.after(3000, lambda: (label.configure(text=''), versao.config(bootstyle="default")))
        return
    data = datetime.now()
    
    texto = f"{version}\n{data}\n{python_version}"
    
    pyinstaller_venv = f"{pyinstaller_path} {spec_path}"
    
    try:
        pyinstaller = subprocess.run(f"{sys.executable} -m pip install pyinstaller", shell=True)
        process = subprocess.Popen(pyinstaller_venv, shell=True)
        versao.config(state='disabled')
        progress_bar.config(mode='indeterminate')
        progress_bar.start()
        while process.poll() is None:
            root.update()
            
        progress_bar.config(mode='determinate')
        progress_var.set(100)
        progress_bar.stop()
        with open('VERSION', 'w') as arquivo:
            arquivo.write(texto)
            
        shutil.copyfile(versao_path, dist_version_path)
        shutil.copyfile(license_path, dist_license_path)
        if os.path.exists(dist_data_path):
            shutil.rmtree(dist_data_path)
        shutil.copytree(data_path, dist_data_path)
        
        list_to_remove = ['auth','users','__pycache__','__init__.py', 'app_config.txt', 'edit_config.py']
        for i in list_to_remove:
            item = os.path.join(os.getcwd(),f'dist/data/{i}')
            try:
                shutil.rmtree(item)
            except:
                try:
                    os.remove(item)
                except:
                    pass
        
        versao.config(state='normal')
        label.config(text='Processo concluído')

    except subprocess.CalledProcessError as e:
        versao.config(state='normal')
        label.config(text=e)

       
root = ttk.Window()
apps = app.Tela(root, 'Peraeque - Build')
root.resizable(False,False)

estilo = ttk.Style(app.Estilo.tema)
fonte = estilo.lookup('Comum.TLabel', 'font')
fonte = int(fonte.split(' ')[1])

adjust_geometry = (fonte / 10)
x = int(round(320 * adjust_geometry))
y = int(round(210 * adjust_geometry))

apps.centralizarTela(x,y)

main_label = ttk.Label(root, text='Build - Applicatas mutant', style='Titulo.TLabel')
sub_label = ttk.Label(root, text='Digite a versão abaixo e clique em Iniciar Processo para gerar o executável', wraplength=320, justify='center', style='Comum.TLabel')
main_label.pack()
sub_label.pack()

progress_var = ttk.IntVar()
progress_bar = ttk.Progressbar(root, mode="determinate", variable=progress_var, length=200)
progress_bar.pack(pady=5)

versao_label = ttk.Label(root, text='Versão',style='Grande.TLabel')
versao_label.pack()

versao_var = ttk.StringVar()
versao = ttk.Entry(root, textvariable=versao_var, style='custom.TEntry')
versao.pack()

label = ttk.Label(root,style='Comum.TLabel')
label.pack()

start_button = ttk.Button(root, text="Iniciar processo", command=run, style="Estilo1.TButton")
start_button.pack(pady=5)

root.mainloop()