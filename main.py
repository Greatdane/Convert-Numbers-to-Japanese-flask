from flask import Flask, render_template, request, jsonify, url_for
from flask_bootstrap import Bootstrap
from convert import web_convert, kanji_dict, kanjiConvert
from num2words import num2words
import os
from flask import send_from_directory

app = Flask(__name__,  static_url_path='/static')
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/basic/')
def basic():
	return render_template('basic.html')

@app.route('/converter/', methods=['POST'])
def converter():
	convert_num = str(request.form.get('convert_number', 0))
	if convert_num == "":
		result = {'kanji':"Please enter either Kanji or Arabic numbers", 'hiragana':"", 'romanji':""}
		return jsonify(result)
	if convert_num[0] in kanji_dict.values():
		try:
			if "点" in convert_num:
				point = convert_num.find("点")
				endNumber = ""
				for x in convert_num[point+1:]:
					endNumber += list(kanji_dict.keys())[list(kanji_dict.values()).index(x)]
				kanji = str(kanjiConvert(convert_num[0:point])) + "." + endNumber
				hiragana = num2words(kanji)
				result = {'kanji':kanji, 'hiragana':hiragana, 'romanji':""}
				return jsonify(result)
			else:
				kanji = str(kanjiConvert(convert_num))
				hiragana = num2words(int(kanji))
				result = {'kanji':kanji, 'hiragana':hiragana, 'romanji':""}
				return jsonify(result)
		except:
			result = {'kanji':"Invalid character, please enter either Kanji or Arabic numbers", 'hiragana':"", 'romanji':""}
			return jsonify(result)

	while convert_num[0] == "0":
		convert_num = convert_num[1:]
	try:
		kanji = web_convert(convert_num, "K")
		hiragana = web_convert(convert_num, "H")
		romanji = web_convert(convert_num, "R")
		result = {'kanji': "Kanji: " + kanji, 'hiragana': "Hiragana: " + hiragana, 'romanji': "Romanji: " + romanji}
		return jsonify(result)
	except:
		result = {'kanji':"Invalid character, please enter either Kanji or Arabic numbers", 'hiragana':"", 'romanji':""}
		return jsonify(result)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
