# progress/utils.py
from progress.models import UserProgress

def complete_section(user, course, section):
    # Get or create progress entry
    progress, created = UserProgress.objects.get_or_create(user=user, course=course)
    
    # Add the section to completed sections if not already added
    if section not in progress.completed_sections.all():
        progress.completed_sections.add(section)
        progress.current_section = section  # Update the current section
        progress.update_progress()  # Update the progress percentage


def answer_question(user, section, question):
    # Get or create progress entry based on section
    progress, created = UserProgress.objects.get_or_create(user=user, current_section=section)
    
    # Add the question to answered questions if not already answered
    if question not in progress.answered_questions.all():
        progress.answered_questions.add(question)
 
def complete_title(user, course, course_title):
    # Get or create progress entry
    progress, created = UserProgress.objects.get_or_create(user=user, course=course)
    
    # Add the title to completed titles if not already added
    if course_title not in progress.completed_title.all():
        progress.completed_title.add(course_title)
        progress.update_progress()  # Update the progress percentage