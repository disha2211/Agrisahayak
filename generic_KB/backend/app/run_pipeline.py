from pathlib import Path

from knowledge_pipeline.config import RAW_HTML_DIR

from knowledge_pipeline.parser import HTMLParser

from knowledge_pipeline.cleaner import HTMLCleaner

from knowledge_pipeline.markdown_builder import MarkdownBuilder

from knowledge_pipeline.normalizer import MarkdownNormalizer

class Pipeline:

    def __init__(self):

        self.parser = HTMLParser()

        self.cleaner = HTMLCleaner()

        self.builder = MarkdownBuilder()

    def run(self,
            crop):

        folder = RAW_HTML_DIR / crop

        html_files = sorted(

            folder.glob("*.html")

        )

        print(f"\nFound {len(html_files)} pages")

        for html in html_files:

            print(f"Processing {html.name}")

            soup = self.parser.parse(html)

            soup = self.cleaner.clean(soup)

            self.builder.add_section(soup)

        normalizer = MarkdownNormalizer()
        markdown = self.builder.merge()
        markdown = normalizer.normalize(markdown)
        metadata = self.builder.metadata(crop,"TNAU")
        output = metadata + markdown
        folder = self.builder.save(crop,output)
        
        print("\nKnowledge base generated successfully.")


if __name__ == "__main__":

    pipeline = Pipeline()

    pipeline.run("tomato")