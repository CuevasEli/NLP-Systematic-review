from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/search', methods=['POST'])
def search():
    keywords = request.form.get('keywords')
    #API asking logic // retrieves topics
    return f"Searched for: {keywords}"


@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
