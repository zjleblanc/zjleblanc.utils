class FilterModule(object):

    def filters(self):
        return { "lsof_parse" : self.do_parse_lsof }

    def do_parse_lsof(self, lsof_raw: list) -> list:
        return self.__parse_lsof_records(lsof_raw)    

    @staticmethod
    def __parse_lsof_records(lines: list) -> dict:
        parsed = {}
        pid = 'ERR'
        file_set_idx = -1
        for line in lines:
            if line[0] == 'p':
                pid = line[1:]
                parsed[pid] = {"pid": pid, "files": []}
                file_set_idx = -1
                continue
            if line[0] == 'f':
                parsed[pid]["files"].append({})
                file_set_idx = len(parsed[pid]["files"]) - 1
                parsed[pid]["files"][file_set_idx]['file_descriptor'] = line[1:]
                continue
            if line[0] == 'a':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['access_mode'] = line[1:]
                    continue
                parsed[pid]['access_mode'] = line[1:]
                continue
            if line[0] == 'c':
                parsed[pid]['command_name'] = line[1:]
                continue
            if line[0] == 'C':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_struct_share_count'] = line[1:]
                continue
            if line[0] == 'd':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_device_character_code'] = line[1:]
                continue
            if line[0] == 'D':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_device_num'] = line[1:]
                continue
            if line[0] == 'F':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_struct_addr'] = line[1:]
                continue
            if line[0] == 'G':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_flags'] = line[1:]
                continue
            if line[0] == 'i':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_inode_num'] = int(line[1:])
                continue
            if line[0] == 'k':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_link_count'] = int(line[1:])
                continue
            if line[0] == 'l':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_lock_status'] = line[1:]
                continue
            if line[0] == 'L':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['proc_login_name'] = line[1:]
                    continue
                parsed[pid]['proc_login_name'] = line[1:]
                continue
            if line[0] == 'n':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_name_comment_addr'] = line[1:]
                continue
            if line[0] == 'N':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['node_identifier'] = line[1:]
                    continue
                parsed[pid]['node_identifier'] = line[1:]
                continue
            if line[0] == 'o':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_offset'] = line[1:]
                continue
            if line[0] == 'g':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['proc_group_id'] = line[1:]
                    continue
                parsed[pid]['proc_group_id'] = line[1:]
                continue
            if line[0] == 'P':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['protocol_name'] = line[1:]
                    continue
                parsed[pid]['protocol_name'] = line[1:]
                continue
            if line[0] == 'r':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['raw_device_number'] = line[1:]
                    continue
                parsed[pid]['raw_device_number'] = line[1:]
                continue
            if line[0] == 'R':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['proc_parent_pid'] = line[1:]
                    continue
                parsed[pid]['proc_parent_pid'] = line[1:]
                continue
            if line[0] == 's':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_size'] = int(line[1:])
                continue
            if line[0] == 'S':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_stream_id'] = line[1:]
                continue
            if line[0] == 't':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['file_type'] = line[1:]
                continue
            if line[0] == 'u':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['proc_user_id'] = line[1:]
                    continue
                parsed[pid]['proc_user_id'] = line[1:]
                continue
            if line[0] == 'Z':
                if file_set_idx >= 0:
                    parsed[pid]["files"][file_set_idx]['selinux_context'] = line[1:]
                    continue
                parsed[pid]['selinux_context'] = line[1:]
                continue
        return parsed