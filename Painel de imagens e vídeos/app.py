import os

from werkzeug.utils import secure_filename

from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, flash

from database.database_adapter import DatabaseAdapter
from utils.aws_s3 import send_file_to_s3, delete_file_from_s3
from utils.file_validations import allowed_file

app = Flask(__name__)
app.secret_key = "no secret needed"

CORS(app)

# pages
index_route = "/"
images_route = "/images"
upload_files_route = "/upload"

# data manipulation endpoints
update_row = "/update"
insert_row = "/insert"
delete_row = "/delete"

# aws
delete_file = '/delete_file'

# -----------------
#  PAGES TEMPLATES
# -----------------


@app.route(index_route)
def index():
    return render_template('index.html')


@app.route(images_route, methods=['GET', 'POST'])
def images_page():
    database = DatabaseAdapter()

    if request.method == 'POST':
        description = request.form['description']
        subject = request.form['subject']

        images = database.query.select_search_files(description, subject)
        page = 1

    else:
        images = database.select_all_joined(
            from_table='images',
            join_table='subjects',
            on=['subject', 'id'],
            columns=['images.id', 'subjects.description', 'subjects.id', 'images.description', 'file_url']
        )
        page = request.args.get('page') or 1
        page = int(page)

    images_per_page = 15
    index_begin = images_per_page * (page-1)
    index_end = images_per_page * page

    try:
        images_paginated = images[index_begin:index_end]
    except:
        total_images = len(images)
        if total_images < images_per_page and page == 1:
            images_paginated = images
        elif index_begin > total_images < index_end:
            images_paginated = images[index_begin:total_images]
        else:
            images_paginated = []

    subjects = database.query.select_all('subjects', '*')

    database.close()
    return render_template(
        'images.html',
        title='Imagens',
        combo_box=subjects,
        multimedia=images_paginated,
        page=int(page)
    )


@app.route(upload_files_route)
def upload_files_page():

    database = DatabaseAdapter()
    subjects = database.query.select_all('subjects', '*')
    database.close()

    return render_template(
        'upload_files.html',
        title='Upload de arquivos',
        submit_route=upload_files_route,
        combo_box=subjects,
        new_value='Novo assunto'
    )


@app.route(upload_files_route, methods=['POST'])
def upload_file():
    database = DatabaseAdapter()

    # Getting html form values
    table = request.form['table']
    subject = request.form['subject']
    description = request.form['description']

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename, table):
            filename = secure_filename(file.filename)
            file.save(os.path.join('', filename))
        else:
            flash(f'Tipo de arquivo inválido!')
            return redirect(request.url)

        bucket = os.environ.get('S3_BUCKET')
        url = f'https://{bucket}.s3-sa-east-1.amazonaws.com/blip-multimedia/{table}/{filename}'

        result = database.persistence.insert_row(
            table=table,
            subject=f"'{subject}'",
            description=f"'{description}'",
            file_url=f"'{url}'"
        )

        database.close()

        if result:
            send_file_to_s3(filename, bucket, table)
            flash("Enviado com sucesso!")
        else:
            flash("Algo deu errado..")

        return redirect(request.url)


# -------------------
#  DATA MANIPULATION
# -------------------


@app.route(update_row)
def update_row_function():
    dml = {
        'table': request.args.get('table'),
        'column': request.args.get('column'),
        'old_id': request.args.get('old_id'),
        'cast': request.args.get('cast')
    }

    sql_cast = dml['cast'] or 'text'

    cols_values = {
        key: value
        for key, value in request.args.items()
        if key not in dml.keys()
    }
    print(cols_values)
    database = DatabaseAdapter()
    update_result = database.persistence.update_by_col(
        table=dml['table'],
        where_col=dml['column'],
        where_value=dml['old_id'],
        cols_values=cols_values,
        cast_to=sql_cast
    )

    if not update_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': update_result['message']
        }

    database.close()
    return update_result


@app.route(insert_row)
def insert_row_function():
    dml = {
        'table': request.args.get('table'),
        'is_combo': request.args.get('is_combo')
    }

    cols_values = {
        key: f"'{value}'"
        for key, value in request.args.items()
        if key not in dml.keys()
    }

    database = DatabaseAdapter()
    insert_result = database.persistence.insert_row(
        table=dml['table'],
        cols_values=cols_values
    )

    if not insert_result:
        database.close()
        return {'status': 'error'}

    if dml['is_combo']:
        combo_values = database.select_all(dml['table'], '*')
        database.close()
        return render_template('combo_box_template.html', combo_box=combo_values, new_value='Novo assunto')

    database.close()
    return insert_result


@app.route(delete_row)
def delete_row_function():
    table = request.args.get('table')
    id = request.args.get('id')
    column = request.args.get('column')

    database = DatabaseAdapter()
    delete_result = database.persistence.delete_by_col(
        table=table,
        where_col=column,
        where_value=id
    )

    if not delete_result['success']:
        database.close()
        return {
            'status': 'error',
            'message': delete_result['message']
        }

    database.close()
    return delete_result


# -------------------
#  AWS MANIPULATION
# -------------------
@app.route(delete_file)
def delete_file_function():
    table = request.args.get('table')
    file_url = request.args.get('file_url')

    delete_file_from_s3(file_url)

    database = DatabaseAdapter()
    delete_result = database.persistence.delete_by_col(table, where_col='file_url', where_value=file_url)

    database.close()
    return delete_result


if __name__ == "__main__":
    from environ import set_environ_variables
    set_environ_variables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
