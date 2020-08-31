def get_title(phrase):
    temp = phrase.split()
    item_name = ""
    if len(temp) > 3:
        for index in range(3):
            item_name += temp[index] 
            item_name += " "
        item_name += "..."
    else:
        item_name = phrase
    return item_name

def gen_info(form):
    hidden_status = set_hidden_status(form)
    status = set_status(form)
    info = {
        'type': form['type'],
        'date': form['date'],
        'account': form['account'],
        'platform': form['platform'],
        'giving': form['giving'],
        'getting': form['getting'],
        'notes': form['notes'],
        'status': status,
        'hidden_status': hidden_status
    }
    return info

def set_hidden_status(form):
    status = ""
    if (form['type'].lower() == 'purchase') and (form['status2'].lower() == 'paid'):
        status = 'pending'
    elif (form['type'].lower() == 'go') and (form['status3'].lower() != 'on the way'):
        status = 'pending'
    elif(form['status1'].lower() == 'on the way') or (form['status2'].lower() == 'on the way') or (form['status3'].lower() == 'on the way'):
        status = 'otw'
    else:
        if(form['type'].lower() == 'trade'):
            status = form['status1'].lower()
        elif(form['type'].lower() == 'purchase'):
            status = form['status2'].lower()
        else:
            status = form['status3'].lower()
    return status

def set_status(form):
    user_status = ""
    if(form['type'].lower() == 'trade'):
        user_status = form['status1']
    elif(form['type'].lower() == 'purchase'):
        user_status = form['status2']
    else:
        user_status = form['status3']
    return user_status
