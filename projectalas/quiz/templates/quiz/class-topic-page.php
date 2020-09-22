{% extends "users/base.php" %}
      {% block content %}
      <div class="edu-accordion-area mg-b-15">
          <div class="container-fluid">
              <div class="row">
                  <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                      <div class="tab-content-details mg-b-30">
                          <h2>{{topics.name}}</h2>
                          <!-- <p>These are the Custom Animate accordion Bootstrap. Using animate bounce, flash, pulse, rubberBand, shake, swing, tada, wobble, jello, bounceIn, bounceInDown, bounceInLeft, bounceInRight, bounceInUp, fadeIn, fadeInDown, fadeInDownBig,
                              fadeInLeft, fadeInLeftBig, fadeInRight, fadeInRightBig, fadeInUp, fadeInUpBig, flipInX, flipInY, lightSpeedIn, rotateIn, rotateInDownLeft, rotateInDownRight, rotateInUpLeft, rotateInUpRight, rollIn, zoomIn, zoomInDown,
                              zoomInLeft, zoomInRight, zoomInUp etc.</p> -->
                      </div>
                  </div>
              </div>

              <div class="row">
                  {% for bc in bcs %}
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                    <div class="courses-inner res-mg-b-30">
                        <h5>{{bc.name}}</h5>
                        <br>
                        <!-- <div class="product-buttons"> -->

                        <a href="{% url 'take_quiz' bc.pk %}" type="button" class="btn-danger cart-btn">Start Quiz</a>
                        <!-- <button onclick="" type="button" class="button-default cart-btn">Read More</button> -->
                      <!-- </div> -->

                        <!-- <p>These are the Custom Animate accordion Bootstrap. Using animate bounce, flash, pulse, rubberBand, shake, swing, tada, wobble, jello, bounceIn, bounceInDown, bounceInLeft, bounceInRight, bounceInUp, fadeIn, fadeInDown, fadeInDownBig,
                            fadeInLeft, fadeInLeftBig, fadeInRight, fadeInRightBig, fadeInUp, fadeInUpBig, flipInX, flipInY, lightSpeedIn, rotateIn, rotateInDownLeft, rotateInDownRight, rotateInUpLeft, rotateInUpRight, rollIn, zoomIn, zoomInDown,
                            zoomInLeft, zoomInRight, zoomInUp etc.</p> -->
                    </div>
                    <br>
                </div>


                  {% endfor %}
          </div>
      </div>
    </div>
{% endblock %}
