import toml


def load_configuration():
    """
    Load the configuration from the 'config.toml' file.

    Returns:
        Tuple[str, str, str, str]: A tuple containing the values of bibtex_file, pdf_path,
        openai_api_key, and md_path respectively.
    """
    config = toml.load("config.toml")

    bibtex_file = config["bibliography"]["path"]
    pdf_path = config["pdf_path"]["path"]
    openai_api_key = config["openai_api_key"]["api_key"]
    md_path = config["md_path"]["path"]

    return bibtex_file, pdf_path, openai_api_key, md_path

