from wtforms.widgets.core import Select, HTMLString, html_params

class SelectDateWidget(object):
  FORMAT_CHOICES = {
    '%d': [(x, str(x)) for x in range(1, 32)],
    '%m': [(1, 'January'),
           (2, 'February'),
           (3, 'March'),
           (4, 'April'),
           (5, 'May'),
           (6, 'June'),
           (7, 'July'),
           (8, 'August'),
           (9, 'September'),
           (10, 'October'),
           (11, 'November'),
           (12, 'December'),
    ],
    '%H': [(x, str(x).zfill(2)) for x in range(0, 24)],  # 24-hour clock zero padded
    '%I': [(x, str(x).zfill(2)) for x in range(1, 13)],  # 12-hour clock zero padded
    '%M': [(x, str(x).zfill(2)) for x in range(0, 59, 15)],  # Minutes zero padded
    '%p': [('AM', 'AM'), ('PM', 'PM')],
  }

  FORMAT_CLASSES = {
   '%d': 'form-control', # 'select_date_day',
   '%m': 'form-control', # 'select_date_month',
   '%Y': 'form-control', # 'select_date_year'
  }

  FORMAT_STYLES = {
    '%d': 'width: 60px', # 'select_date_day',
    '%m': 'width: 120px', # 'select_date_month',
    '%Y': 'width: 80px', # 'select_date_year'
    '%H': 'width: 60px',
    '%I': 'width: 60px',
    '%M': 'width: 60px',
    '%p': 'width: 60px',
  }

#  def __init__(self, years=range(2014, 1930, -1)):
  def __init__(self):
    super(SelectDateWidget, self).__init__()
#    self.FORMAT_CHOICES['%Y'] = [(x, str(x)) for x in years]

  def __call__(self, field, **kwargs):
    field_id        = kwargs.pop('id', field.id)
    html            = []
    allowed_format  = ['%d', '%m', '%Y', '%H', '%I', '%M', '%p']

    # Handle custom year ranges
    startyear = 2010
    endyear = 2020
    if 'startyear' in field.description:
        startyear = int(field.description['startyear'])
    if 'endyear' in field.description:
        endyear = int(field.description['endyear'])

    self.FORMAT_CHOICES['%Y'] = [(x, str(x)) for x in range(endyear, startyear, -1)]


    html.append('<div class="form-inline">')
    for format in field.format.split():
      if (format in allowed_format):
        choices     = self.FORMAT_CHOICES.get(format, [(None, 'Invalid Format')])
        id_suffix   = format.replace('%', '-')
        id_current  = field_id + id_suffix

        kwargs['class'] = self.FORMAT_CLASSES.get('format', 'form-control')
#        kwargs['class'] = 'form-control'
        kwargs['style'] = self.FORMAT_STYLES.get(format, '')
        try: del kwargs['placeholder']
        except: pass

        html.append('<select %s>' % html_params(name=field.name, id=id_current, **kwargs))

        if field.data:
            try: current_value = int(field.data.strftime(format))
            except: current_value = field.data.strftime(format)
        else:
            current_value = None

        for value, label in choices:
          selected = (value == current_value)
          html.append(Select.render_option(value, label, selected))
        html.append('</select>')
      else:
        html.append(format)
        html.append('<input type="hidden" value="'+format+'" %s></input>' % html_params(name=field.name, id=id_current, **kwargs))

      html.append(' ')

    html.append('</div>')

    return HTMLString(''.join(html))

# Display a Select group as a Button Group (Bootstrap)    
class ButtonGroupWidget(object):
  def __call__(self, field, **kwargs):
    field_id        = kwargs.pop('id', field.id)
    html            = []
    classes         = kwargs.get('class', '')

    html.append('<div class="btn-group btn-group-md" style="border: none;" data-toggle="buttons">')

    if field.data:
        current_value = field.data
    else:
        current_value = None
    
    for value, label in field.choices:
        active = ''
        checked = ''
        if str(value) == str(current_value):
            active = ' active'
            checked = ' checked'
#        html.append('%r == %r' % (str(value), current_value))
        
        html.append('<label class="btn btn-default%s">' % active)
        html.append('<input type="radio" class="%s" name="%s" value="%s" %s /> %s' % (classes, field_id, value, checked, label))
        html.append("</label>\n")

    html.append('</div>')

    return HTMLString(''.join(html))

# Display a Select group as a Button Group (Bootstrap)    
class BooleanButtonWidget(object):
  def __call__(self, field, **kwargs):
    field_id        = kwargs.pop('id', field.id)
    html            = []

    html.append('<div class="btn-group btn-group-md" style="border: none;" data-toggle="buttons">')

    if field.data:
        current_value = field.data
    else:
        current_value = None
    
    for value, label in field.choices:
        active = ''
        checked = ''
        if (current_value and str(value) in ['1', 'Yes', 'True']) or \
           (not current_value and str(value) in ['0', 'No', 'False', 'None']):
            active = ' active'
            checked = ' checked'
        
#        html.append('%r == %r' % (str(value), current_value))
        html.append('<label class="btn btn-default%s">' % active)
        html.append('<input type="radio" name="%s" value="%s" %s /> %s' % (field_id, value, checked, label))
        html.append("</label>\n")

    html.append('</div>')

    return HTMLString(''.join(html))
