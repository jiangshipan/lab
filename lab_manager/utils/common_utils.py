from datetime import datetime


# form校验器
def validate_form(form):
    if not form.validate():
        errors = [u'有错误发生:']
        for k, v in form.errors.items():
            for m in v:
                errors.append(u'%s:%s' % (getattr(form, k).label.text, m))
        raise Exception(u'<br/>'.join(errors))


def time2datetime(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    time_str = '2020-12-22 12:00:00'
    d = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    print(type(d))