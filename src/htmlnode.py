class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag: '{self.tag}', value: '{self.value}', children: '{self.children}', props: '{self.props}')"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if (self.props is None) or (self.props == {}):
            return ""
        else:
            attrs = ""
            for key in self.props:
                attrs = f'{attrs} {key}="{self.props[key]}"'
            return attrs


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have at least one child.")

        result = f"<{self.tag}>"
        for child in self.children:
            result = f"{result}{child.to_html()}"
        result = f"{result}</{self.tag}>"
        return result


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode(tag: '{self.tag}', value: '{self.value}', props: '{self.props}')"

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

