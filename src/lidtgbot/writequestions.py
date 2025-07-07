"""Writes questions to firestore"""
import json
import asyncio
from lidtgbot.database.question import question_repository
from lidtgbot.database.translation import TranslationRepository





async def write_questions_to_firestore():

    with open("data/questions.json", "r") as file:
        d = json.load(file)
        for question in d:
            num = question['num']
            solution = question['solution']
            category = question['category']
            image = question.get('image')
            if image == '-':
                image = None

            # Create the question in Firestore
            try:                
                await question_repository.create_question(num, solution, category, image)
                print(f"Question {num} created successfully")
                translation_repository = TranslationRepository(num)
                # Create translations for each language
                await translation_repository.create_translation(
                        language_code='de',
                        question=question['question'],
                        context=question.get('context'),
                        option_a=question['a'],
                        option_b=question['b'],
                        option_c=question['c'],
                        option_d=question['d']
                    )
                for lang, translation in question.get('translation', {}).items():
                    await translation_repository.create_translation(
                        language_code=lang,
                        question=translation['question'],
                        context=translation.get('context'),
                        option_a=translation['a'],
                        option_b=translation['b'],
                        option_c=translation['c'],
                        option_d=translation['d']
                    )

            except Exception as e:
                print(f"Failed to create question {num}: {e}")


if __name__ == "__main__":
    asyncio.run(write_questions_to_firestore())
