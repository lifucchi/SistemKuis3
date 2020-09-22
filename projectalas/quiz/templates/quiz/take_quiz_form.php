{% extends 'users/base.php' %}

{% load crispy_forms_tags %}

{% block css %}
<style type="text/css">
/* https://jsbin.com/zequb/7/edit */
input[type=radio]{
  /* hide original inputs */
  visibility: hidden;
  position: absolute;
}
input[type=radio] + label{
  cursor:pointer;
}
input[type=radio] + label:before{
  width:16px;
  height:16px;
  content: " ";
  display:inline-block;
  border:1px solid #ccc;
  border-radius:50%;
  box-shadow: inset 0 -3px 6px #e4e4e4;
  transition: 0.3s;
}

/* CHECKED */
input[type=radio]:checked + label:before{
  box-shadow: inset 0 0 0 5px #2196F3;
}
</style>
{% endblock %}

{% block content %}
<div class="edu-accordion-area mg-b-15">
    <div class="container-fluid">
  <div class="progress mb-3">
    <div class="progress-bar" role="progressbar" aria-valuenow="{{ progress }}" aria-valuemin="0" aria-valuemax="100" style="width: {{ progress }}%"></div>
  </div>
  <h2><span class="badge badge-secondary">{{ answered_questions|add:"1" }}/{{total_questions}}</span></h2>

  <h2 class="mb-3">{{ quiz.name }}</h2>
  <p class="lead">{{ question.label }}</p>
  <form  method="post" novalidate>
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">Next →</button>
  </form>

</div>
</div>
{% endblock %}
