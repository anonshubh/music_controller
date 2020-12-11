import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from 'react-router-dom';

import CreateRoomPage from './CreateRoomPage'
import RoomJoinPage from './RoomJoinPage'

class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }
    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path='/'><p>The Home Page</p></Route>
                    <Route path='/join' component={RoomJoinPage} />
                    <Route path='/create' component={CreateRoomPage} />
                </Switch>
            </Router>
        );
    }
}

export default HomePage;
