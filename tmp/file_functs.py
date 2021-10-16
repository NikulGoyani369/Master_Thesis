import glob

def get_list_of_file_names():
    return glob.glob("./tmp/semeval2013-Task7-2and3way/*/2way/*/*.xml") + \
           glob.glob("./tmp/semeval2013-Task7-2and3way/test/2way/*/*/*.xml")


def extract_data(st):
    files = get_list_of_file_names()
    try:
        f = open(f'{files[st.session_state.count]}', 'r')
        data = f.read()
    except IndexError:
        st.session_state.count = 0
        f = open(f'{files[st.session_state.count]}', 'r')
        data = f.read()
    return data