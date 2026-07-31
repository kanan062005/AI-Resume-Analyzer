import re


class BulletRewriter:

    @staticmethod
    def rewrite(text):

        bullets = []

        lines = text.split("\n")

        action_words = {
            "worked": "Developed",
            "made": "Designed",
            "created": "Engineered",
            "used": "Leveraged",
            "did": "Implemented",
            "built": "Built",
            "developed": "Developed"
        }

        for line in lines:

            line = line.strip()

            if len(line) < 8:
                continue

            if line.startswith("-") or line.startswith("•"):

                sentence = line[1:].strip()

            else:
                sentence = line

            words = sentence.split()

            if len(words) == 0:
                continue

            first = words[0].lower()

            if first in action_words:

                words[0] = action_words[first]

            sentence = " ".join(words)

            if not sentence.endswith("."):
                sentence += "."

            if "%" not in sentence and "accuracy" not in sentence.lower():

                sentence += (
                    " Achieved measurable improvements in performance."
                )

            bullets.append(sentence)

        return bullets