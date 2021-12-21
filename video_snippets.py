import pandas


class VideoSnippets:
    def __init__(self, data_as_csv):
        self.data_as_csv = data_as_csv
        self.init_data()

    def init_data(self):
        try:
            pandas.read_csv('video_snippets.csv')
        except FileNotFoundError:
            data = pandas.DataFrame(dict(title=[], link=[]))
            data.to_csv(self.data_as_csv, index=False)

    def data(self):
        return pandas.read_csv(self.data_as_csv)

    def add(self, title, link):
        data = self.data()
        data.loc[len(data.index)] = [title, link]
        data.to_csv(self.data_as_csv, index=False)
        print(f"\n{data}\n")

    def remove(self, idx):
        data = self.data()
        data = data.drop(index=idx)
        data.to_csv(self.data_as_csv, index=False)

        if not data.empty:
            print(f"\n{data}\n")
