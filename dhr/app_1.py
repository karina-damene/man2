from flask import Flask, render_template

# importing pandas module
import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
tableau_1 = pd.DataFrame(data=d)
tableau_1 = tableau_1.to_html(index=False)


d = {'col3': [41, 42], 'col4': [43, 24]}
tableau_1_summary = pd.DataFrame(data=d)

number = tableau_1_summary.iloc[0,0]
print(type(number))

dhr="CK062529"
lot = 2237
quantite_totale_fabriquee = 168
quantite_rebutee = 0
quantite_de_produits_conformes = quantite_totale_fabriquee - quantite_rebutee
reference = 22177
reference_dm = "yl079100"
indice_manu = "ref2"
indice_add = ""
tableau_1_summary = tableau_1_summary.to_html(index=False)


app = Flask(__name__)
@app.route('/')
@app.route('/table')
def table():
    return render_template('table.html', page_title_text='eDHR',
                       title_text='eDHR _ Device History Record',
                       #text =':DHR - [Référence DM] - [Lot]',
                       #<p>DHR - {{dhr}} - {{lot}}<strong>{{text}}</strong>
                       dhr = dhr,
                       lot = lot,
                       quantite_totale_fabriquee = quantite_totale_fabriquee,
                       quantite_rebutee = quantite_rebutee,
                       quantite_de_produits_conformes = quantite_de_produits_conformes,
                       reference = reference,
                       reference_dm= reference_dm,
                       indice_manu= indice_manu,
                       indice_add=indice_add,
                       prices_text='Historical prices of S&P 500',
                       stats_text='Historical prices summary statistics',
                       tableau_1=tableau_1,
                       tableau_1_summary=tableau_1_summary,
                       show_number='show number',
                       number = number)



if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))

