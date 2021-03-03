class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.ver = ver
        self.ext = ext

    # Added @property with the 'filename' composite
    # ver now has up to 3 digits
    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    # Added @property with the 'path' composite
    @property
    def path(self):
        result = self.folder_path + "/" + self.filename
        return result


# now prints path
scene_file = SceneFile("D:\\", "tank", "model", 1, ".ma")
print(scene_file.filename)
print(scene_file.path)
