import argparse
from ppt_translator import PPTTranslator

def main():
    parser = argparse.ArgumentParser(description='Translate PowerPoint files')
    parser.add_argument('input', help='Input PPT file path')
    parser.add_argument('output', help='Output PPT file path')
    parser.add_argument('--lang', default='zh', help='Target language code (default: zh)')
    parser.add_argument('--api-key', required=True, help='DeepSeek API key')
    
    args = parser.parse_args()
    
    translator = PPTTranslator(api_key=args.api_key)
    translator.translate_ppt(args.input, args.output, args.lang)
    
if __name__ == '__main__':
    main()  
