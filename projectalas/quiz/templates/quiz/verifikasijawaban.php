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
<form  method="post">
    {% csrf_token %}
    <input type="hidden" name="verifikasi" value="1">
    {% for a in useranswer %}
        <div class="card border border-primary">
            <div class="card-body">
                <div class="content" style="display:flex">
                    <div class="blocktext" style="flex-basis: 50%;" >
                        <h4 style="color:black"  >{{ a.question.label }}</h4>
                        <ul style="list-style: none;">
                            {% for choice in a.choices %}
                                {% if choice.id == a.answer.answer.id %}
                                    <li style="color:green">
                                        {{ choice.label }}
                                            [ Jawaban Kamu ]
                                    </li>
                                {% else %}
                                    <li>
                                        {{ choice.label }}
                                    </li>
                                {% endif %}
                            {% endfor %}
                        </ul>
                    </div>
                    <div style="flex-basis:50%; border-left:1px solid black; padding-left:10px;">
                        <h4 style="color:black">Apakah Kamu menjawab pertanyaan di samping dengan menebak (ngasal / nyontek)? Isilah dengan jujur!</h4>
                        <input required oninvalid="this.setCustomValidity('Mohon pilih ya / tidak')" oninput="this.setCustomValidity('')" type="radio" id="yes-{{ a.question.id }}" name="{{ a.answer.id }}" value="1">
                        <label for="yes-{{ a.question.id }}">Ya, saya menjawab pertanyaan disamping dengan menebak</label><br>
                        <input required oninvalid="this.setCustomValidity('Mohon pilih ya / tidak')" oninput="this.setCustomValidity('')"  type="radio" id="no-{{ a.question.id }}" name="{{ a.answer.id }}" value="0">
                        <label for="no-{{ a.question.id }}">Tidak, sudah saya hitung</label><br>
                    </div>
                </div>
            </div>
        </div>
        <br>
    {% endfor %}

<button  type="submit" class="btn btn-coklat" >Selanjutnya →</button>
</form>
{% endblock %}
