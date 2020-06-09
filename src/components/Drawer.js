import React, { Fragment } from 'react';

import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

export default function Drawer() {
  const menuItems = ['Politics', 'Tech', 'Entertainment', 'Travel', 'Sports'];
  const list = (trigger) => {
    <Fragment role="presentation">
    menuItems.map((text, index) => (
      <ListItem button key={index}>
          <List primary={text}>
      </ListItem>
    ));
    </Fragment>
  }
  
  return ()
}
