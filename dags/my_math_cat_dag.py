from pendulum import datetime
from airflow.decorators import dag, task
from operators.basic_math_operator import MyBasicMathOperator
from hooks.cat_fact_hook import CatFactHook


@dag(
    schedule_interval="@daily",
    start_date=datetime(2021, 1, 1),
    # render Jinja template as native Python object
    render_template_as_native_obj=True,
    catchup=False,
)
def my_math_cat_dag():
    add = MyBasicMathOperator(
        task_id="add",
        first_number=23,
        second_number=19,
        operation="+",
        # any BaseOperator arguments can be used with the custom operator too
        doc_md="Addition Task.",
    )

    substract = MyBasicMathOperator(
        task_id="substract",
        # use the return value from the add task as the first_number, pulling from XCom
        first_number="{{ ti.xcom_pull(task_ids='add', key='return_value') }}",
        second_number=35,
        operation="-",
    )

    @task
    def use_cat_fact_hook(number):
        num_catfacts_needed = round(number)
        # instatiating a CatFactHook at runtime of this task
        hook = CatFactHook("cat_fact_conn")
        hook.log_cat_facts(num_catfacts_needed)

    add >> substract >> use_cat_fact_hook(substract.output)


my_math_cat_dag()