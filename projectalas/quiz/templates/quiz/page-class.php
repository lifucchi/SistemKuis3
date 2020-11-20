{% extends "quiz/base.php" %}
      {% block content %}
      <div class="row">

        {% for cc in ccs %}

          <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <strong class="card-title">Kelas {{ cc.classes }}</strong>
                </div>
                <div class="card-body">
                  <p class="card-text">{{cc.name}}</p>
                  <button onclick="location.href = '{% url 'topics' pk=cc.id %}';" type="button" class="btn btn-primary" style="float: right;"><i class="fa fa-star"></i>&nbsp;Selengkapnya</button>
                </div>
            </div>
        </div>

      {% endfor %}

      </div>

{% endblock %}
