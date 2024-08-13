from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

# Dados simulados para tópicos e comentários
topics = [
    {
        'id': 1,
        'title': 'Bem-vindo ao Fórum',
        'content': 'Este é o primeiro tópico do fórum.',
        'comments': [
            {'content': 'Obrigado! Feliz por estar aqui.'}
        ]
    }
]

# Função para obter o próximo ID de tópico
def get_next_id():
    return max(topic['id'] for topic in topics) + 1

@app.route('/')
def index():
    return render_template('index.html', topics=topics)

@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = next((topic for topic in topics if topic['id'] == topic_id), None)
    if topic is None:
        return 'Tópico não encontrado', 404
    return render_template('topic.html', topic=topic)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_topic = {
            'id': get_next_id(),
            'title': title,
            'content': content,
            'comments': []
        }
        topics.append(new_topic)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/topic/<int:topic_id>/comment', methods=['POST'])
def comment(topic_id):
    topic = next((topic for topic in topics if topic['id'] == topic_id), None)
    if topic is None:
        return 'Tópico não encontrado', 404
    content = request.form['content']
    topic['comments'].append({'content': content})
    return redirect(url_for('topic', topic_id=topic_id))

if __name__ == '__main__':
    app.run(debug=True)
