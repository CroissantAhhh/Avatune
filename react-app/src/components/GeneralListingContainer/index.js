import { useState, useEffect } from 'react';

import GeneralListing from "../GeneralListing"


export default function GeneralListingContainer({ title, listings, compact, category }) {
    const [displayedListings, setDisplayedListings] = useState(listings)

    useEffect(() => {
        if (compact && listings.length > 5) {
            setDisplayedListings(listings.slice(4))
        }
    }, [])

    return (
        <div className="listings-container l-vertical">
            <div className="title-container">
                <p>{title}</p>
            </div>
            <div className="listings-section l-horizontal">
                {displayedListings.map(listing => (
                    <GeneralListing key={listing.hashedId} item={listing} category={category} />
                ))}
            </div>
        </div>
    )
}
