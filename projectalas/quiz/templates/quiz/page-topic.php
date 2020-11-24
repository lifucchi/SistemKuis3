{% extends "quiz/base.php" %}
      {% block content %}
      <div class="row">

        {% for bc in bcs %}

          <div class="col-lg-12">
            <div class="card">
                <div class="card-header">
                    <strong class="card-title">{{ topic_name }}</strong>
                </div>
                <div class="card-body">
                  <p class="card-text">{{bc.name}}</p>
                  {% if bc.roll_out == 1 %}
                  <button onclick="location.href = '{% url 'take_quiz' pk=bc.pk %}';" type="button" class="btn btn-primary" style="float: right;"><i class="fa fa-star"></i>&nbsp;Mulai Kuis</button>
                  {% else %}
                  <button onclick="location.href = '{% url 'take_quiz' pk=bc.pk %}';" type="button" class="btn btn-primary "  disabled="" style="float: right;"><i class="fa fa-star"></i>&nbsp;Mulai Kelas</button>
                  {% endif %}
                </div>
            </div>
        </div>

      {% endfor %}

      </div>

{% endblock %}
