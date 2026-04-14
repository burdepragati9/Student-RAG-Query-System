from langchain_community.document_loaders import DirectoryLoader, CSVLoader

def load_data():
    loader = DirectoryLoader(
        "./data",
        glob="**/*.csv",
        loader_cls=CSVLoader
    )
    return loader.load()