class FilterModule(object):

    def filters(self):
        return { "lsof_parse" : self.do_parse_lsof }

    def do_parse_lsof(self, lsof_raw: list) -> list:
        return self.__parse_lsof_records(lsof_raw)    

    @staticmethod
    def __parse_lsof_records(lines: list) -> dict:
        parsed = []
        process = None
        file = None
        for line in lines:
            if line[0] == 'p':
                pid = line[1:]
                process = { "pid": int(pid) }
                file = None
                continue
            if line[0] == 'f':
                if file:
                    parsed.append(file)
                file = { "file_descriptor": line[1:] }
                file.update(process)
                continue
            if line[0] == 'a':
                if file:
                    file['access_mode'] = line[1:]
                    continue
                process['access_mode'] = line[1:]
                continue
            if line[0] == 'c':
                process['command_name'] = line[1:]
                continue
            if line[0] == 'C':
                if file:
                    file['file_struct_share_count'] = line[1:]
                continue
            if line[0] == 'd':
                if file:
                    file['file_device_character_code'] = line[1:]
                continue
            if line[0] == 'D':
                if file:
                    file['file_device_num'] = line[1:]
                continue
            if line[0] == 'F':
                if file:
                    file['file_struct_addr'] = line[1:]
                continue
            if line[0] == 'G':
                if file:
                    file['file_flags'] = line[1:]
                continue
            if line[0] == 'i':
                if file:
                    file['file_inode_num'] = int(line[1:])
                continue
            if line[0] == 'k':
                if file:
                    file['file_link_count'] = int(line[1:])
                continue
            if line[0] == 'l':
                if file:
                    file['file_lock_status'] = line[1:]
                continue
            if line[0] == 'L':
                if file:
                    file['proc_login_name'] = line[1:]
                    continue
                process['proc_login_name'] = line[1:]
                continue
            if line[0] == 'n':
                if file:
                    file['file_name'] = line[1:]
                continue
            if line[0] == 'N':
                if file:
                    file['node_identifier'] = line[1:]
                    continue
                process['node_identifier'] = line[1:]
                continue
            if line[0] == 'o':
                if file:
                    file['file_offset'] = line[1:]
                continue
            if line[0] == 'g':
                process['proc_group_id'] = int(line[1:])
                continue
            if line[0] == 'P':
                if file:
                    file['protocol_name'] = line[1:]
                    continue
                process['protocol_name'] = line[1:]
                continue
            if line[0] == 'r':
                if file:
                    file['raw_device_number'] = line[1:]
                    continue
                process['raw_device_number'] = line[1:]
                continue
            if line[0] == 'R':
                process['proc_parent_pid'] = int(line[1:])
                continue
            if line[0] == 's':
                if file:
                    file['file_size'] = int(line[1:])
                continue
            if line[0] == 'S':
                if file:
                    file['file_stream_id'] = line[1:]
                continue
            if line[0] == 't':
                if file:
                    file['file_type'] = line[1:]
                continue
            if line[0] == 'u':
                process['proc_user_id'] = int(line[1:])
                continue
            if line[0] == 'Z':
                if file:
                    file['selinux_context'] = line[1:]
                    continue
                process['selinux_context'] = line[1:]
                continue

        if file:
            parsed.append(file)

        return parsed