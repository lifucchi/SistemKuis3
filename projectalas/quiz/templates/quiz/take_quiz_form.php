{% extends 'quiz/base3.php' %}

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

.content {
  max-width: 500px;
  margin: auto;
}

.center {
  text-align: center;
  border: 3px solid green;
}

/* .center {
  text-align: center;
  border: 3px solid green;
} */

.blocktext {
    margin-left: auto;
    margin-right: auto;
    width: 8em
}

.asteriskField {
    display: none;
}


</style>
{% endblock %}

{% block content %}
{% if question %}
<!-- <div class="content ">
    <div class="blocktext" style="text-align: center"  >
  <h4  style="color:black"  >{{ answered_questions|add:"1" }} . {{ question.label }}</h4>
  <form  method="post" novalidate>
    {% csrf_token %}
    {{ form|crispy }}
    <button  onclick="return confirm('Menuju ke soal selanjutnya?')" type="submit" class="btn btn-coklat" >Selanjutnya →</button>
  </form>

</div>
</div> -->

<div class="card border border-primary">
  <div class="card-body">
    <div class="content ">
        <div class="blocktext" style="text-align: center"  >
      <h4  style="color:black"  >{{ answered_questions|add:"1" }} . {{ question.label }}</h4>
      <form  method="post" novalidate>
        <input type="hidden" name="starttime" id="starttimeformat">
        <input type="hidden" name="endtime" id="endtimeformat">
        {% csrf_token %}
        {{ form|crispy }}
        <button  onclick="return confirm('Menuju ke soal selanjutnya?')" type="submit" class="btn btn-coklat" >Selanjutnya →</button>
      </form>

    </div>
    </div>
  </div>

</div>

{% endif %}
{% endblock %}
