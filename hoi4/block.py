from typing import Optional

class Blocks:
    
    cls_tokens = []
    cls_loc = 0
    cur_lvl = 0
    
    @classmethod
    def set_tokens(cls, tokens, loc = 0):
        cls.cls_tokens = tokens
        cls.cls_loc = loc
    
    def __init__(self, name, start_loc: int,parent_lvl:Optional[int]):
        self.name = name
        self.start_loc = start_loc
        self.lvl = self.get_lvl(parent_lvl)
        self.sub_blocks = {}
        self.dict_or_list = self.judge_sub_type()
        self.contents = self.get_contents()
        
    
    def get_lvl(self, parent_lvl:Optional[int]):
        if parent_lvl is None:
            lvl = 0
        else:
            lvl = parent_lvl + 1
        return lvl
    

    def judge_sub_type(self):
        if Blocks.cls_loc == 0:
            return 'dict'
        
        if self.start_loc > len(Blocks.cls_tokens) - 3:
            return 'list'
        
        else:
            first_two_token = Blocks.cls_tokens[self.start_loc + 1:self.start_loc+3]
            if '=' in first_two_token:
                return 'dict'
            else:
                return 'list'
    
    def get_contents(self):
        if self.dict_or_list == 'dict':
            return {}
        else:
            return []
    
    def add_to_dict(self,key,val):
        key = self.get_dict_key(key)
        self.contents[key] = val
    
    def get_dict_key(self, key):
        n = 1
        while key in self.contents.keys():
            key = f'{key}__{n}'
            n += 1
        return key
    
    def parse_tokens(self):
        while Blocks.cls_loc < len(Blocks.cls_tokens):
            token = Blocks.cls_tokens[Blocks.cls_loc]
                
            if token == "}":
                return
            
            else:
                if self.dict_or_list == 'list':
                    if token == "{":
                        sub_class = self.get_subblock()
                        self.sub_blocks[sub_class.name] = sub_class
                    else:
                        self.contents.append(token)
                    # Blocks.cls_loc += 1
                
                else:
                    if token == "=":
                        Blocks.cls_loc += 1
                        token = Blocks.cls_tokens[Blocks.cls_loc]
                    
                        if token == "{":
                            sub_class = self.get_subblock()
                            self.sub_blocks[sub_class.name] = sub_class
                            self.add_to_dict(sub_class.name,sub_class.contents)
                            
                        elif token == "player_countries": #debug index to delete
                            pass

                        else:
                            self.add_to_dict(Blocks.cls_tokens[Blocks.cls_loc-2],Blocks.cls_tokens[Blocks.cls_loc])
                            # Blocks.cls_loc += 1
                
                Blocks.cls_loc += 1
    
    def get_subblock(self):
        name = Blocks.cls_tokens[Blocks.cls_loc-2] # -1 is always =
        # assert Blocks.cls_tokens[Blocks.cls_loc-1] == "=", "No = found"
        # assert Blocks.cls_tokens[Blocks.cls_loc -2], "No name found"

        sub_class = Blocks(name, Blocks.cls_loc, self.lvl)
        Blocks.cls_loc += 1
        sub_class.parse_tokens()
        return sub_class
        
        



