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

                </div>
            </div>
        </div>

      {% endfor %}

      </div>

{% endblock %}
