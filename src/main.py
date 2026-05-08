import os
import shutil

from convert_md import markdown_to_html_node


def copy_source(source_path="static", dest_path="public", is_root=True):
    if is_root:
        print("Copying files...")

    cwd = os.getcwd()
    source_path = os.path.join(cwd, source_path)
    dest_path = os.path.join(cwd, dest_path)

    # Check if `source_path` is valid
    if not os.path.exists(source_path):
        raise Exception("invalid source path")

    # If `dest_path` directory is present, delete it
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    # Recreate `dest_path` directory
    os.mkdir(dest_path)

    for entry in os.listdir(source_path):
        source_entry_path = os.path.join(source_path, entry)
        dest_entry_path = os.path.join(dest_path, entry)
        if os.path.isfile(source_entry_path):
            shutil.copy(source_entry_path, dest_entry_path)
        else:
            copy_source(source_entry_path, dest_entry_path, is_root=False)

    if is_root:
        print("Copied files successfully!")


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            print("Extracted title successfully!")
            return line[2:]
    print("Function failed; no h1/# header found")
    raise Exception("no h1/# header found")


def generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html"):
    print(f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}`...")

    # Get full paths
    cwd = os.getcwd()
    from_path = os.path.join(cwd, from_path)
    template_path = os.path.join(cwd, template_path)
    dest_path = os.path.join(cwd, dest_path)

    with open(from_path, "r") as f:
        from_content = f.read()
    print(f"Read from `{from_path}`")

    with open(template_path, "r") as f:
        template_content = f.read()
    print(f"Read from `{template_path}`")

    # Extract title and create HTML
    title = extract_title(from_content)
    html = markdown_to_html_node(from_content).to_html()

    # Use template but replace title and content fields
    page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Check if `dest_dirname` directory exists; if not, create it
    dest_dirname = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)
        print(f"`{dest_path}` directory did not exist; created directory.")

    # Write `page` contents to `dest_path` file path
    with open(dest_path, "w") as f:
        f.write(page)

    print("File generated and written successfully!")


def main():
    copy_source("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()

