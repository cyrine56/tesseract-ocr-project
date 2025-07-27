# main.py
import argparse
from converters.text_to_pdf import txt_to_pdf
from converters.image_to_text import image_to_text

parser = argparse.ArgumentParser(description="Outil de conversion de fichiers")

parser.add_argument("--mode", choices=["txt2pdf", "img2txt"], required=True)
parser.add_argument("--input", required=True)
parser.add_argument("--output", help="Chemin du fichier de sortie (si nécessaire)")

args = parser.parse_args()

if args.mode == "txt2pdf":
    if not args.output:
        print("Veuillez spécifier le fichier PDF de sortie avec --output")
    else:
        txt_to_pdf(args.input, args.output)
        print(f"[✓] {args.input} → {args.output}")
elif args.mode == "img2txt":
    result = image_to_text(args.input)
    print("[Texte détecté]:\n", result)
