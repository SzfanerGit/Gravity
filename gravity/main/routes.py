from unicodedata import name
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from gravity import db
from gravity.database import Satelite, Plot
from gravity.main.forms import AddSateliteForm, GeneratePlotForm
from gravity.main.utils import save_trans_plot ,convert_to_list
from gravity.simulation.main import Body, Earth, plot_satelites

main = Blueprint('main', __name__)


@main.route("/home")
@main.route("/", methods=['GET', 'POST'])
def home():
    # Default plot
    plot_image = url_for('static', filename='orbit_plots/Example_orbit.png')

    # Formm to input satelites by pos and vel
    form = AddSateliteForm()
    if form.validate_on_submit():
        # logged in user adds satelites to database
        if current_user.is_authenticated:
            satelite = Satelite(name=form.name.data, pos_0=form.pos.data, vel_0=form.vel.data, user_id=current_user.id)
            db.session.add(satelite)
            db.session.commit()
            flash(f'Satelite added', 'success')
            return redirect(url_for('main.home'))
        # non user generates plot on subbmit
        else:
            pos = convert_to_list(form.pos.data)
            vel = convert_to_list(form.vel.data)
            sat = Body(pos, vel, central_body=Earth)
            p_path = plot_satelites([sat,], save=True, filename='temp')
            p_name = save_trans_plot(p_path, random=False)
            plot_image = url_for('static', filename='orbit_plots/' + p_name)

    plot_form = GeneratePlotForm()
    # get satelites owned by the user
    try:
        user_satelites = Satelite.query.filter_by(user_id=current_user.id)
    except:
        user_satelites = []

    # logged in user can generate all satelites and change view angle here
    if current_user.is_authenticated:
        if plot_form.validate_on_submit():
            # Formating: view angles
            v_angle = convert_to_list(plot_form.view_angles.data, target=2)
            # and satelites to plot
            sats = []
            for satelite in user_satelites:
                pos = convert_to_list(satelite.pos_0)
                vel = convert_to_list(satelite.vel_0)
                sats.append(Body(pos, vel, central_body=Earth))

            # Generate and save plot for the current user
            # plot_satelites automatically calcultes their paths
            p_path = plot_satelites(sats, view_angle=v_angle ,save=True, filename='temp')
            p_name = save_trans_plot(p_path, random=True)
            plot_image = url_for('static', filename='orbit_plots/' + p_name)
            # save to the database (TODO Is it actually needed?)
            plot = Plot(plot_image=plot_image, user_id=current_user.id)
            db.session.add(plot)
            db.session.commit()

    return render_template('home.html', form=form, plot_form=plot_form, 
                           user_satelites=user_satelites, plot_image=plot_image)


@main.route("/satelite/<int:satelite_id>/delete", methods=['POST'])
@login_required
def delete_satelite(satelite_id):
    satelite = Satelite.query.get_or_404(satelite_id)
    # .owner is a backref to the user data (lookup in database.py User)
    if satelite.owner != current_user:
        abort(403)
    db.session.delete(satelite)
    db.session.commit()
    flash('Satelite was deleted from the list!', 'success')

    return redirect(url_for('main.home'))




@main.route("/about")
def about():
    return render_template('about.html')
