from textnode import TextNode, TextType


def main():
    exampleNode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )

    print(exampleNode)


if __name__ == "__main__":
    main()
