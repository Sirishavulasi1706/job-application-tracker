from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app import db

from app.models import CareerChat

from app.services.career_chat_service import (
    ask_career_assistant
)

career_chat = Blueprint(
    "career_chat",
    __name__
)


@career_chat.route(
    "/career-chat",
    methods=["GET", "POST"]
)
@login_required
def chat():

    answer = None

    if request.method == "POST":

        question = request.form["message"]

        answer = ask_career_assistant(question)

        conversation = CareerChat(

            user_id=current_user.id,

            user_message=question,

            ai_response=answer

        )

        db.session.add(conversation)

        db.session.commit()

        flash(
            "Response generated successfully!",
            "success"
        )

    return render_template(
        "career_chat.html",
        answer=answer
    )


@career_chat.route("/career-chat/history")
@login_required
def history():

    chats = (
        CareerChat.query
        .filter_by(user_id=current_user.id)
        .order_by(CareerChat.created_at.desc())
        .all()
    )

    return render_template(
        "chat_history.html",
        chats=chats
    )


@career_chat.route(
    "/career-chat/delete/<int:id>"
)
@login_required
def delete_chat(id):

    chat = CareerChat.query.get_or_404(id)

    db.session.delete(chat)

    db.session.commit()

    flash(
        "Conversation deleted.",
        "success"
    )

    return redirect(
        url_for("career_chat.history")
    )