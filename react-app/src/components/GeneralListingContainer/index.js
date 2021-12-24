import { useState, useEffect } from 'react';

import GeneralListing from "../GeneralListing"

import './GeneralListingContainer.css';

export default function GeneralListingContainer({ title, listings, category }) {

    return (
        <div className="general-listings-container l-vertical">
            <div className="title-container">
                <p className="title-container-text">{title}</p>
            </div>
            <div className="general-listings-section">
                {listings.map(listing => (
                    <GeneralListing key={listing.hashedId} item={listing} category={category} />
                ))}
            </div>
        </div>
    )
}
