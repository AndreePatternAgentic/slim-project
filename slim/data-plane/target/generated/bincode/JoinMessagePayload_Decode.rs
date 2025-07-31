impl < __Context > :: bincode :: Decode < __Context > for JoinMessagePayload
{
    fn decode < __D : :: bincode :: de :: Decoder < Context = __Context > >
    (decoder : & mut __D) ->core :: result :: Result < Self, :: bincode ::
    error :: DecodeError >
    {
        core :: result :: Result ::
        Ok(Self
        {
            channel_name : :: bincode :: Decode :: decode(decoder) ?,
            channel_id : :: bincode :: Decode :: decode(decoder) ?,
            moderator_name : :: bincode :: Decode :: decode(decoder) ?,
        })
    }
} impl < '__de, __Context > :: bincode :: BorrowDecode < '__de, __Context >
for JoinMessagePayload
{
    fn borrow_decode < __D : :: bincode :: de :: BorrowDecoder < '__de,
    Context = __Context > > (decoder : & mut __D) ->core :: result :: Result <
    Self, :: bincode :: error :: DecodeError >
    {
        core :: result :: Result ::
        Ok(Self
        {
            channel_name : :: bincode :: BorrowDecode ::< '_, __Context >::
            borrow_decode(decoder) ?, channel_id : :: bincode :: BorrowDecode
            ::< '_, __Context >:: borrow_decode(decoder) ?, moderator_name :
            :: bincode :: BorrowDecode ::< '_, __Context >::
            borrow_decode(decoder) ?,
        })
    }
}