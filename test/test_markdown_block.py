import unittest

from src.markdown_block import block_to_block_type, BLOCK_TYPE, markdown_to_blocks, markdown_to_html_node


class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        test_cases = [
            ("# This is a heading", BLOCK_TYPE.HEADING),
            ("This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
             BLOCK_TYPE.PARAGRAPH),
            ("""* This is the first list item in a list block
* This is a list item
* This is another list item""", BLOCK_TYPE.UNORDERED_lIST),
            ("""1. This is the first list item in a list block
2. This is a list item
3. This is another list item""", BLOCK_TYPE.ORDERED_LIST)
        ]

        for test in test_cases:
            self.assertEqual(block_to_block_type(test[0]), test[1])

    def test_markdown_to_blocks(self):
        para = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        self.assertListEqual(markdown_to_blocks(para), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ])

    def test_markdown_to_html(self):
        para = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```
        """
        print(markdown_to_html_node(para).to_html())


if __name__ == '__main__':
    unittest.main()
