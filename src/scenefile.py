from pathlib import Path  # Makes Paths into a Path object


class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = Path(folder_path)   # now a 'Path' object
        self.descriptor = descriptor
        self.task = task
        self.ver = ver
        self.ext = ext

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    # Now will use proper slashes in path name
    @property
    def path(self):
        return self.folder_path / self.filename


scene_file = SceneFile("D:/", "tank", "model", 1, ".ma")
print(scene_file.path)  # prints D:\tank_model_v001.ma
