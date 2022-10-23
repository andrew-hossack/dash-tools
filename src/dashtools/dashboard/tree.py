import os
from dash_iconify import DashIconify
import dash_mantine_components as dmc


class FileTree:

    def __init__(self, filepath: os.PathLike, initial_state={'0': True}):
        self.filepath = filepath
        self.state = initial_state

    def render(self) -> dmc.Accordion:
        return dmc.Accordion(
            self.build_tree(self.filepath, isRoot=True),
            iconPosition='right',
            state=self.state,
            multiple=True,
            id='filetree-accordion-id')

    def flatten(self, l):
        return [item for sublist in l for item in sublist]

    def make_file(self, file_name):
        return dmc.Text(
            [DashIconify(icon="akar-icons:file"), " ", file_name], style={"paddingTop": '5px'}
        )

    def make_folder(self, folder_name):
        return [DashIconify(icon="akar-icons:folder"), " ", folder_name]

    def build_tree(self, path, isRoot=False):
        d = []
        if os.path.isdir(path):
            children = self.flatten([self.build_tree(os.path.join(path, x))
                                    for x in os.listdir(path)])
            if isRoot:
                d.append(
                    dmc.AccordionItem(
                        children=children,
                        label=self.make_folder(os.path.basename(path)))
                )
            else:
                d.append(
                    dmc.Accordion(children=[
                        dmc.AccordionItem(
                            children=children,
                            label=self.make_folder(os.path.basename(path)))
                    ],
                        iconPosition='right',
                        multiple=True)
                )
        else:
            d.append(self.make_file(os.path.basename(path)))
        return d
