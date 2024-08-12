class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children
            and self.props == other.props
        ):
            return True
        return False

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(map(lambda x: f" {x[0]}=\"{x[1]}\"", self.props.items()))

    def __repr__(self):
        return f"{self.__class__.__name__}(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props:{self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, props, value=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("Value is empty")

        if self.tag is None or self.tag == "":
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, props, children=None, tag=""):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == "" or self.tag is None:
            raise ValueError("tag is empty")
        if self.children is None:
            raise ValueError("Must have children")

        new_line = ""
        return f"<{self.tag}{self.props_to_html()}>{new_line.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"




    
