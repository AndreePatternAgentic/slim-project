impl :: bincode :: Encode for JoinMessagePayload
{
    fn encode < __E : :: bincode :: enc :: Encoder >
    (& self, encoder : & mut __E) ->core :: result :: Result < (), :: bincode
    :: error :: EncodeError >
    {
        :: bincode :: Encode :: encode(&self.channel_name, encoder) ?; ::
        bincode :: Encode :: encode(&self.channel_id, encoder) ?; :: bincode
        :: Encode :: encode(&self.moderator_name, encoder) ?; core :: result
        :: Result :: Ok(())
    }
}