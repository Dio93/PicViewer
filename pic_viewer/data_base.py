import os

class DataBase:
    def __init__(self, path):
        def _is_pic(src):
            if len(src) >=5:
                if src[-5:] in [".jpeg"]:
                    return True
            if len(src) >= 4:
                    if src[-4:] in [".png", ".jpg"]:
                        return True
            return False
        
        self.db = {}
        self.tags = set()
        self.filtered = []
        
        try:
            with open(path, encoding="UTF-8") as db_file:
                self.db = {line.split(";")[0]:line.split(";")[1].replace("\n","") for line in db_file if len(line.split(";")) >= 2}
                db_file.close()
        except:
            print("No database found")

        # load all files in db
        files = [dirpath + "\\" + filename for (dirpath, dirnames, filenames) \
                  in os.walk(os.getcwd()) for filename in filenames]
        
        off = len(os.getcwd())
        self.db = {src:self.db[src] if src in self.db else "".join(t.replace("_", " ") + "," for t in src[off:].split("\\")[:-1] \
                                                    if len(t)>0) for src in files if _is_pic(src)}
        
        self.tags = {t.strip() for d in self.db.values() for t in d.split(",") if len(t)>0}
        self.filtered = [src for src, tags in self.db.items()]
    
    def filter(self, filter_tags):
        def _has_tags(tags, filter_tags):
            filter_tags = [ft.strip() for ft in filter_tags.split(",") if len(ft)>0]
            tags = [tag.strip() for tag in tags.split(",") if len(tag)>0]
            # print("filter\n", filter_tags)
            # print("tags\n", tags)
            for each in filter_tags:
                if each not in tags:
                    return False
            return True
        
        self.filtered = [src for src, tags in self.db.items() if _has_tags(tags, filter_tags)]
