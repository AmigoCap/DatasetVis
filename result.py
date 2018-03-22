import time
import settings as st
import prediction as pr

# Initialization of output json
def init_result():
    json_result = {
        'timestamp': time.time(),
        'settings': {
            'size': st.size,
            'offset_test': st.offset_test,
            'offset_train_val': st.offset_train_val,
            'nb_epoch': st.nb_epoch,
            'batch_size': st.batch_size,
            'learning_rate': st.learning_rate,
            'nb_filter': st.nb_filter,
            'filter_size': st.filter_size,
            'reseau': st.reseau
        },
        'results': [],
        'confusion': [],
        'metrics': []
    }
    return json_result
