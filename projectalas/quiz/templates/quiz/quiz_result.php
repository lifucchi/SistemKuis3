{% extends 'users/base.html' %}
{% load quiz_extras %}

{% block content %}
<!-- {% include 'classroom/students/_header.html' with active='taken' %} -->

<h2>{{quiz.name}}</h2>
<!-- {{ quiz.subject.get_html_badge }} -->

<div class="progress">
  <div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: {{percentage}}%" aria-valuenow="{{percentage}}" aria-valuemin="0" aria-valuemax="100">{{percentage}}%</div>
</div><br>
{% for question in questions %}
<div class="card">
  <div class="card-body">
    <h5 class="card-title">{{forloop.counter}}. {{question.label}}</h5>
    <table class="table table-bordered table-sm">
      <thead><tr><th>Yours</th><th>Correct</th><th></th></tr></thead>
      <tbody>
        {% for opt in question.answers.all %}
        {% marked_answer user opt as opt_marked %}
        <tr>
          <td style="width: 100px;{% if opt_marked == 'correct' %} background:green{% elif opt_marked == 'wrong' %} background:red{% endif %}"> </td>
          <td style="width: 100px;{% if opt.is_correct %} background:green{% endif %}"></td>
          <td>{{opt.text}}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
<br>
{% endfor %}
{% endblock %}
