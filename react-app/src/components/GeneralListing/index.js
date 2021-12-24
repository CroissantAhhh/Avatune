import { useHistory } from 'react-router-dom';

import "./GeneralListing.css";

// A general container element for a variety of resources
// Category can be one of: Medium, Artist, Album, Playlist, User
export default function GeneralListing({ item, category }) {
    const history = useHistory();

    function redirect() {
        history.push(`/${category.toLowerCase()}/${item.hashedId}`)
    };

    return (
        <div className="general-listing hover-pointer" onClick={redirect}>
            <img src={item.image} alt="item image/artwork" height="200px" width="200px"></img>
            <div className="general-listing-text">
                <p className="general-listing-title">{item.title}</p>
                <p className="general-listing-category">{category}</p>
            </div>
        </div>
    )
}
