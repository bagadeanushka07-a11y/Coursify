from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .forms import QuizForm, QuestionForm
from .models import Quiz, Question, QuizAttempt

from courses.models import Course
from enrollments.models import Enrollment


# =========================================================
# INSTRUCTOR ACCESS HELPER
# =========================================================

def instructor_required(request):

    return request.user.is_authenticated and request.user.role in [
        "instructor",
        "admin"
    ]


# =========================================================
# INSTRUCTOR COURSES
# =========================================================

def get_instructor_courses(request):

    if request.user.role == "admin":

        return Course.objects.all()

    return Course.objects.filter(
        instructor=request.user
    )


# =========================================================
# QUIZ LIST
# =========================================================

@login_required
def quiz_list(request):

    if instructor_required(request):

        quizzes = Quiz.objects.filter(
            course__in=get_instructor_courses(request)
        ).select_related(
            "course"
        ).order_by(
            "-created_at"
        )

    else:

        # Students can see quizzes for courses
        # they are enrolled in.

        quizzes = Quiz.objects.filter(
            course__enrollments__student=request.user
        ).select_related(
            "course"
        ).distinct().order_by(
            "-created_at"
        )

    return render(
        request,
        "quizzes/quiz_list.html",
        {
            "quizzes": quizzes
        }
    )


# =========================================================
# CREATE QUIZ
# =========================================================

@login_required
def create_quiz(request):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to create quizzes."
        )

        return redirect("dashboard")

    courses = get_instructor_courses(request)

    if request.method == "POST":

        form = QuizForm(request.POST)

        form.fields["course"].queryset = courses

        if form.is_valid():

            quiz = form.save(
                commit=False
            )

            # Security check:
            # selected course must belong to instructor

            if quiz.course not in courses:

                messages.error(
                    request,
                    "You can only create quizzes for your own courses."
                )

                return redirect("quiz_list")

            quiz.save()

            messages.success(
                request,
                "Quiz created successfully!"
            )

            return redirect(
                "manage_quiz",
                quiz_id=quiz.id
            )

    else:

        form = QuizForm()

        form.fields["course"].queryset = courses

    return render(
        request,
        "quizzes/quiz_form.html",
        {
            "form": form,
            "page_title": "Create Quiz",
            "button_text": "Create Quiz",
        }
    )


# =========================================================
# EDIT QUIZ
# =========================================================

@login_required
def edit_quiz(request, quiz_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to edit quizzes."
        )

        return redirect("dashboard")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        course__in=get_instructor_courses(request)
    )

    courses = get_instructor_courses(request)

    if request.method == "POST":

        form = QuizForm(
            request.POST,
            instance=quiz
        )

        form.fields["course"].queryset = courses

        if form.is_valid():

            updated_quiz = form.save(
                commit=False
            )

            if updated_quiz.course not in courses:

                messages.error(
                    request,
                    "You can only use your own courses."
                )

                return redirect(
                    "manage_quiz",
                    quiz_id=quiz.id
                )

            updated_quiz.save()

            messages.success(
                request,
                "Quiz updated successfully!"
            )

            return redirect(
                "manage_quiz",
                quiz_id=quiz.id
            )

    else:

        form = QuizForm(
            instance=quiz
        )

        form.fields["course"].queryset = courses

    return render(
        request,
        "quizzes/quiz_form.html",
        {
            "form": form,
            "quiz": quiz,
            "page_title": "Edit Quiz",
            "button_text": "Save Changes",
        }
    )


# =========================================================
# DELETE QUIZ
# =========================================================

@login_required
def delete_quiz(request, quiz_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to delete quizzes."
        )

        return redirect("dashboard")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        course__in=get_instructor_courses(request)
    )

    if request.method == "POST":

        quiz_title = quiz.title

        quiz.delete()

        messages.success(
            request,
            f'Quiz "{quiz_title}" deleted successfully.'
        )

        return redirect(
            "quiz_list"
        )

    return render(
        request,
        "quizzes/quiz_confirm_delete.html",
        {
            "quiz": quiz
        }
    )


# =========================================================
# MANAGE QUIZ
# =========================================================

@login_required
def manage_quiz(request, quiz_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to manage quizzes."
        )

        return redirect("dashboard")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        course__in=get_instructor_courses(request)
    )

    questions = quiz.questions.all().order_by(
        "id"
    )

    question_count = questions.count()

    attempt_count = quiz.attempts.count()

    return render(
        request,
        "quizzes/manage_quiz.html",
        {
            "quiz": quiz,
            "questions": questions,
            "question_count": question_count,
            "attempt_count": attempt_count,
        }
    )


# =========================================================
# ADD QUESTION
# =========================================================

@login_required
def add_question(request, quiz_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to add questions."
        )

        return redirect("dashboard")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        course__in=get_instructor_courses(request)
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST
        )

        if form.is_valid():

            question = form.save(
                commit=False
            )

            question.quiz = quiz

            question.save()

            messages.success(
                request,
                "Question added successfully!"
            )

            return redirect(
                "manage_quiz",
                quiz_id=quiz.id
            )

    else:

        form = QuestionForm()

    return render(
        request,
        "quizzes/question_form.html",
        {
            "form": form,
            "quiz": quiz,
            "page_title": "Add Question",
            "button_text": "Add Question",
        }
    )


# =========================================================
# EDIT QUESTION
# =========================================================

@login_required
def edit_question(request, question_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to edit questions."
        )

        return redirect("dashboard")

    question = get_object_or_404(
        Question,
        id=question_id,
        quiz__course__in=get_instructor_courses(request)
    )

    quiz = question.quiz

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Question updated successfully!"
            )

            return redirect(
                "manage_quiz",
                quiz_id=quiz.id
            )

    else:

        form = QuestionForm(
            instance=question
        )

    return render(
        request,
        "quizzes/question_form.html",
        {
            "form": form,
            "quiz": quiz,
            "question": question,
            "page_title": "Edit Question",
            "button_text": "Save Changes",
        }
    )


# =========================================================
# DELETE QUESTION
# =========================================================

@login_required
def delete_question(request, question_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to delete questions."
        )

        return redirect("dashboard")

    question = get_object_or_404(
        Question,
        id=question_id,
        quiz__course__in=get_instructor_courses(request)
    )

    quiz_id = question.quiz.id

    if request.method == "POST":

        question.delete()

        messages.success(
            request,
            "Question deleted successfully!"
        )

        return redirect(
            "manage_quiz",
            quiz_id=quiz_id
        )

    return render(
        request,
        "quizzes/question_confirm_delete.html",
        {
            "question": question
        }
    )


# =========================================================
# QUIZ ATTEMPTS
# =========================================================

@login_required
def quiz_attempts(request, quiz_id):

    if not instructor_required(request):

        messages.error(
            request,
            "You do not have permission to view quiz attempts."
        )

        return redirect("dashboard")

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        course__in=get_instructor_courses(request)
    )

    attempts = QuizAttempt.objects.filter(
        quiz=quiz
    ).select_related(
        "student"
    ).order_by(
        "-attempted_at"
    )

    return render(
        request,
        "quizzes/quiz_attempts.html",
        {
            "quiz": quiz,
            "attempts": attempts,
        }
    )


# =========================================================
# QUIZ DETAIL / START QUIZ
# =========================================================

@login_required
def quiz_detail(request, quiz_id):

    quiz = get_object_or_404(
        Quiz.objects.select_related(
            "course"
        ).prefetch_related(
            "questions"
        ),
        id=quiz_id
    )

    # -----------------------------------------------------
    # INSTRUCTOR CHECK
    # -----------------------------------------------------

    is_instructor = (
        request.user.role in [
            "instructor",
            "admin"
        ]
        and
        quiz.course.instructor == request.user
    )

    # -----------------------------------------------------
    # STUDENT ENROLLMENT CHECK
    # -----------------------------------------------------

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=quiz.course
    ).exists()

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not is_instructor and not is_enrolled:

        messages.error(
            request,
            "You must be enrolled in this course to attempt the quiz."
        )

        return redirect(
            "course_detail",
            course_id=quiz.course.id
        )

    questions = quiz.questions.all()

    return render(
        request,
        "quizzes/quiz_detail.html",
        {
            "quiz": quiz,
            "questions": questions,
        }
    )


# =========================================================
# SUBMIT QUIZ
# =========================================================

# =========================================================
# SUBMIT QUIZ
# =========================================================

@login_required
def submit_quiz(request, quiz_id):

    # -----------------------------------------------------
    # ONLY POST REQUESTS
    # -----------------------------------------------------

    if request.method != "POST":

        return redirect(
            "quiz_detail",
            quiz_id=quiz_id
        )

    # -----------------------------------------------------
    # GET QUIZ
    # -----------------------------------------------------

    quiz = get_object_or_404(
        Quiz.objects.select_related(
            "course"
        ).prefetch_related(
            "questions"
        ),
        id=quiz_id
    )

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    is_instructor = (
        request.user.role in [
            "instructor",
            "admin"
        ]
        and
        quiz.course.instructor == request.user
    )

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=quiz.course
    ).exists()

    if not is_instructor and not is_enrolled:

        messages.error(
            request,
            "You are not enrolled in this course."
        )

        return redirect(
            "course_detail",
            course_id=quiz.course.id
        )

    # -----------------------------------------------------
    # GET QUESTIONS
    # -----------------------------------------------------

    questions = quiz.questions.all()

    total_questions = questions.count()

    score = 0

    results = []

    # -----------------------------------------------------
    # CHECK ANSWERS
    # -----------------------------------------------------

    for question in questions:

        selected_answer = request.POST.get(
            f"question_{question.id}"
        )

        is_correct = (
            selected_answer == question.correct_answer
        )

        if is_correct:
            score += 1

        # -------------------------------------------------
        # SELECTED ANSWER TEXT
        # -------------------------------------------------

        if selected_answer == "A":

            selected_text = question.option_a

        elif selected_answer == "B":

            selected_text = question.option_b

        elif selected_answer == "C":

            selected_text = question.option_c

        elif selected_answer == "D":

            selected_text = question.option_d

        else:

            selected_text = "Not answered"

        # -------------------------------------------------
        # CORRECT ANSWER TEXT
        # -------------------------------------------------

        if question.correct_answer == "A":

            correct_text = question.option_a

        elif question.correct_answer == "B":

            correct_text = question.option_b

        elif question.correct_answer == "C":

            correct_text = question.option_c

        elif question.correct_answer == "D":

            correct_text = question.option_d

        else:

            correct_text = question.correct_answer

        # -------------------------------------------------
        # STORE RESULT
        # -------------------------------------------------

        results.append(
            {
                "question": question,
                "selected_answer": selected_answer,
                "selected_text": selected_text,
                "correct_answer": question.correct_answer,
                "correct_text": correct_text,
                "is_correct": is_correct,
            }
        )

    # -----------------------------------------------------
    # CALCULATE PERCENTAGE
    # -----------------------------------------------------

    if total_questions > 0:

        percentage = int(
            (score / total_questions) * 100
        )

    else:

        percentage = 0

    # -----------------------------------------------------
    # PASS / FAIL
    # -----------------------------------------------------

    passing_percentage = 50

    passed = percentage >= passing_percentage

    # -----------------------------------------------------
    # SAVE QUIZ ATTEMPT
    # -----------------------------------------------------

    QuizAttempt.objects.create(
        quiz=quiz,
        student=request.user,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        passed=passed
    )

    # -----------------------------------------------------
    # RESULT PAGE
    # -----------------------------------------------------

    return render(
        request,
        "quizzes/quiz_result.html",
        {
            "quiz": quiz,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "passed": passed,
            "results": results,
        }
    )