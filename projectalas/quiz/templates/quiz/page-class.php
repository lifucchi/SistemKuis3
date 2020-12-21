{% extends "quiz/base.php" %}
      {% block content %}
      <div class="row">

        {% for cc in ccs %}

          <div class="col-md-6">
            <div class="card">
                <div class="card-header" style="background-color:#967259;">
                    <strong class="card-title" style="color:#ece0d1" >Kelas {{ cc.classes }}</strong>
                </div>
                <div class="card-body">
                  <p class="card-text">{{cc.name}}</p>
                  <button onclick="location.href = '{% url 'topics' pk=cc.id %}';" type="button" class="btn btn-coklat" style="float: right;"><i class="fa fa-star"></i>&nbsp;Selengkapnya</button>
                </div>
            </div>
        </div>

      {% endfor %}

      </div>

{% endblock %}
