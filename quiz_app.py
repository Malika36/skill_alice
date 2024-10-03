from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Простой список вопросов и ответов
questions = [
    {
        "question": "Какой язык программирования используется для разработки веб-приложений на стороне сервера?",
        "options": ["Python", "JavaScript", "HTML", "CSS"],
        "answer": "Python"
    },
    {
        "question": "Кто является создателем Python?",
        "options": ["Linus Torvalds", "Guido van Rossum", "Bjarne Stroustrup", "James Gosling"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "Что такое API?",
        "options": ["ООП", "Программный интерфейс для приложений", "Набор данных", "Серверная база данных"],
        "answer": "Программный интерфейс для приложений"
    },
]


@app.route('/post', methods=['POST'])
def post():
    req = request.json
    session = req['session']
    user_command = req['request']['command'].lower()

    # Ожидаем начала викторины
    if 'начать викторину' in user_command:
        question = random.choice(questions)
        response_text = f"Вопрос: {question['question']} Варианты: {', '.join(question['options'])}"
        session['current_question'] = question
        session['is_quiz_active'] = True

    # Проверка ответа пользователя
    elif session.get('is_quiz_active'):
        if user_command in [option.lower() for option in session['current_question']['options']]:
            if user_command.capitalize() == session['current_question']['answer']:
                response_text = "Верно! Молодец! Хотите ещё вопрос?"
            else:
                response_text = "Неправильно. Правильный ответ: " + session['current_question']['answer']
            session['is_quiz_active'] = False  # Завершаем викторину

        else:
            response_text = "Выберите один из предложенных вариантов."

    else:
        response_text = "Пожалуйста, скажите 'начать викторину', чтобы начать."

    return jsonify({
        "version": req['version'],
        "session": session,
        "response": {
            "text": response_text,
            "end_session": False
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
