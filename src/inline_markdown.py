import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
                result.append(node)
        else:
            sections = node.text.split(delimiter)
            if (len(sections) % 2) == 0:
                raise Exception(f"Invalid `markdown`: formatted section not closed.")
            for i in range(0, len(sections)):
                if (i % 2) == 0:
                    result.append(TextNode(sections[i], TextType.TEXT))
                else:
                    result.append(TextNode(sections[i], text_type))
    return result


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            images = extract_markdown_images(node.text)
            if not images:
                result.append(node)
                continue
            remaining_text = node.text
            for image in images:
                search_str = f"![{image[0]}]({image[1]})"
                sections = remaining_text.split(search_str, 1)
                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))
                remaining_text = sections[1]
            if remaining_text != "":
                result.append(TextNode(remaining_text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            links = extract_markdown_links(node.text)
            if not links:
                result.append(node)
                continue
            remaining_text = node.text
            for link in links:
                search_str = f"[{link[0]}]({link[1]})"
                sections = remaining_text.split(search_str, 1)
                if sections[0] != "":
                    result.append(TextNode(sections[0], TextType.TEXT))
                result.append(TextNode(link[0], TextType.LINK, link[1]))
                remaining_text = sections[1]
            if remaining_text != "":
                result.append(TextNode(remaining_text, TextType.TEXT))
    return result


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    text = [TextNode(text, TextType.TEXT)]
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "_", TextType.ITALIC)
    text = split_nodes_delimiter(text, "`", TextType.CODE)
    text = split_nodes_image(text)
    text = split_nodes_link(text)
    return text

